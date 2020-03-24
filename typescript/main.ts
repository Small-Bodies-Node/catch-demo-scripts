// Import library modules
import * as EventSource from 'eventsource';
import axios from 'axios';
import * as fs from 'fs';

// Params for CATCH query
const ROOT_URL = "https://catch.astro.umd.edu/catch/";
const isRefreshed = !false;
const isVerbose = !true;
const pauseBetweenStartOfGetObjidDataMs = 1500;

// Build an array of target objects to fetch data for (65P -> 69P)
// This script will not check for existence of such objids
// An empty array of results will be returned if objid not found
let objids = [];
for (let i = 70; i < 85; i++) {
    objids.push(i + 'P');
}
// objids = ["65P"];


// The script's main logic has to be placed in an async function in order to use
// JS async/await syntax. Using JS promises in this way helps avoid 'callback hell'.
async function main() {
    // Map each objid to a process to fetch that data; all done in parallel (for load testing)


    for (let i = 0; i < objids.length; i++) {
        //
        console.log("######");
        getObjidData(objids[i]).catch(err => {
            console.log("An error occurred. Are you connected to internet?");
            console.log("Error: ", err.message);
            process.exit(1);
        });
        await new Promise(resolve => setTimeout(resolve, pauseBetweenStartOfGetObjidDataMs));

    }
}
// Run main function
main();



async function getObjidData(objid: string) {

    console.log("FETCHING DATA FOR", objid);

    // Stage 1
    // Run a conventional HTTP Request to the '/catch/query/moving' route to
    // query if target data already exists, is cached, or to force a recomputation of the data
    if (isVerbose) console.log("Running Stage 1", objid);
    const res1 = await axios.get(ROOT_URL + `query/moving?target=${objid}${isRefreshed ? '&cached=false' : ''}`);
    const data1 = res1.data;
    let jobId: string = data1.job_id;
    if (isVerbose) console.log("data1", data1);


    // Stage 2
    // If we just triggered a (re-)computation of the target data, then launch
    // a "Big Query" that listens to Server-Sent Events until the query is finished
    // and a new job_id is returned
    if (data1.isQueueFull) {
        console.log("Queue is full! Stopping", objid);
        return;
    }
    else if (!!data1.queued) {
        if (isVerbose) console.log("Running Stage 2", objid);
        if (isVerbose) console.log("An expensive query has been launched. This typically takes 5-30 seconds to complete!!!");
        jobId = await pingCatchServerSentEventEndPoint(jobId);
        if (isVerbose) console.log("The query has finished!", jobId);
    } else {
        if (isVerbose) console.log("Skipping Stage 2", objid);
    }

    // Stage 3
    // Use our jobId to retrieve the actual data, now available via a conventional http request
    if (isVerbose) console.log("Running Stage 3", objid);
    const res3 = await axios.get(ROOT_URL + `caught/${jobId}`);
    const dataPlusMeta = res3.data;
    // console.log("data", jobId, dataPlusMeta);

    // Stage 4
    // Output data to json file
    if (isVerbose) console.log("Running Stage 4", objid);
    const filename = 'output_' + objid + '.json'
    fs.writeFileSync(filename, JSON.stringify(dataPlusMeta, null, 2));


    console.log(`Data download finished and saved in ${filename}`);

    return dataPlusMeta;

}



// Wrap SSE-callback sequence with async function that returns a JS promise
async function pingCatchServerSentEventEndPoint(jobId: string): Promise<string> {

    const url = ROOT_URL + 'stream';
    // console.log('jobId', jobId, url);

    return new Promise<string>(resolve => {

        // Create new SSE source with the node EventSource API
        const source = new EventSource(ROOT_URL + 'stream');

        // Act on messages sent from server
        source.onmessage = function (msgEvent: MessageEvent) {

            // Do sth generic with SSE message
            if (isVerbose) console.log('msgEvent', msgEvent, msgEvent.data, typeof msgEvent);

            // If message returned with our jobId, then close SSE connection
            if (msgEvent.data === jobId) {
                this.close(); // Sever connection to SSE route
                resolve(msgEvent.data); // Return jobId as resolved Promise
            }
        };
    });
}




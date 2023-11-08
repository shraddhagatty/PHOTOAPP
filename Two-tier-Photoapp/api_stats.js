//
// app.get('/stats', async (req, res) => {...});
//
// return some stats about our bucket and database:
//
const dbConnection = require('./database.js')
const { HeadBucketCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

exports.get_stats = async (req, res) => {

  console.log("call to /stats...");

  try {

    //
    // build input object with request parameters:
    //
    var input = {
      Bucket: s3_bucket_name
    };

    //
    // calling S3 to get bucket status, returning a PROMISE
    // we have to wait on eventually:
    //
    console.log("/stats: calling S3...");

    var command = new HeadBucketCommand(input);
    var s3_response = s3.send(command);

    //
    // calling RDS to get # of users and # of assets. For 
    // consistency, we turn the DB call with callback into
    // a PROMISE so we can wait for it while we wait for
    // the S3 response:
    //
    var rds_response = new Promise((resolve, reject) => {
      try {
        console.log("/stats: calling RDS...");

        var sql = `
          Select count(*) As NumUsers From users;
          Select count(*) As NumAssets From assets;
          `;

        dbConnection.query(sql, (err, results, _) => {
          try {
            if (err) {
              reject(err);
              return;
            }

            console.log("/stats query done");
            resolve(results);
          }
          catch (code_err) {
            reject(code_err);
          }
        });
      }
      catch (code_err) {
        reject(code_err);
      }
    });

    //
    // nothing else to do, so let's asynchronously wait
    // for the promises to resolve / reject:
    //
    Promise.all([s3_response, rds_response]).then(results => {
      try {
        // we have a list of results, so break them apart:
        var s3_result = results[0];
        var rds_results = results[1];

        // extract the s3 result:
        var metadata = s3_result["$metadata"];

        // extract the db result, which is a list of lists:
        var rows_r1 = rds_results[0];  // first list:
        var rows_r2 = rds_results[1];  // second list:

        // each list from db has exactly one row:
        var row_r1 = rows_r1[0];  // first row:
        var row_r2 = rows_r2[0];  // first row:

        //
        // done, respond with stats:
        //
        console.log("/stats done, sending response...");

        res.json({
          "message": "success",
          "s3_status": metadata["httpStatusCode"],
          "db_numUsers": row_r1["NumUsers"],
          "db_numAssets": row_r2["NumAssets"]
        });
      }
      catch (code_err) {
        res.status(400).json({
          "message": code_err.message,
          "s3_status": -1,
          "db_numUsers": -1,
          "db_numAssets": -1
        });
      }
    }).catch(err => {
      //
      // we get here if calls to S3 or RDS failed, or we
      // failed to process the results properly:
      //
      res.status(400).json({
        "message": err.message,
        "s3_status": -1,
        "db_numUsers": -1,
        "db_numAssets": -1
      });
    });

  }//try
  catch (err) {
    //
    // generally we end up here if we made a 
    // programming error, like undefined variable
    // or function:
    //
    res.status(400).json({
      "message": err.message,
      "s3_status": -1,
      "db_numUsers": -1,
      "db_numAssets": -1
    });
  }//catch

}//get

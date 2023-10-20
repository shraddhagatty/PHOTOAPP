//
// app.get('/users', async (req, res) => {...});
//
// Return all the users from the database:
//
const dbConnection = require('./database.js')
const { HeadBucketCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

exports.get_users = async (req, res) => {

  console.log("call to /users...");

  try {


    //throw new Error("TODO: /users");

    //
    // TODO: remember we did an example similar to this in class with
    // movielens database (lecture 05 on Thursday 04-13)
    //
    // MySQL in JS:
    //   https://expressjs.com/en/guide/database-integration.html#mysql
    //   https://github.com/mysqljs/mysql
    //
    //
    // build input object with request parameters:
    //
    var input = {
      Bucket: s3_bucket_name
    };


    // calling RDS to get all users  in ascending order 
    // ,we turn the DB call with callback into
    // a PROMISE so we can wait for it while we wait for
    // the S3 response:
    //
    var rds_response = new Promise((resolve, reject) => {
      try {
        console.log("/users: calling RDS...");

        var sql = `
          Select * from users order by userid asc;
          `;

        dbConnection.query(sql, (err, results, _) => {
          try {
            if (err) {
              reject(err);
              return;
            }

            console.log("/users query done");
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


    Promise.all([rds_response]).then(results => {
      try {
        // we have a list of results, so break them apart:
        //var rds_results = results[0];


        // extract the db result, which is a list of lists:
        var rows = results[0];  // first list:

        //
        // done, respond with users:
        //
        console.log("/users done, sending response...");

        res.json({
          "message": "success",
          "data": rows
        });
      }
      catch (code_err) {
        res.status(400).json({
          "message": code_err.message,
          "data": []
        });
      }
    }).catch(err => {
      //
      // we get here if calls to S3 or RDS failed, or we
      // failed to process the results properly:
      //
      res.status(400).json({
        "message": err.message,
        "data": []
      });
    });

  }//try
  catch (err) {
    res.status(400).json({
      "message": err.message,
      "data": []
    });
  }//catch

}//get

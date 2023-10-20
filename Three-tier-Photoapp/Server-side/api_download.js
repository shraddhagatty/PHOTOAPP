//
// app.get('/download/:assetid', async (req, res) => {...});
//
// downloads an asset from S3 bucket and sends it back to the
// client as a base64-encoded string.
//
const dbConnection = require('./database.js')
const { GetObjectCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');
const { url } = require('inspector');

exports.get_download = async (req, res) => {

  console.log("call to /download...");

  try {


    //throw new Error("TODO: /download/:assetid");

    //
    // TODO
    //
    // MySQL in JS:
    //   https://expressjs.com/en/guide/database-integration.html#mysql
    //   https://github.com/mysqljs/mysql
    // AWS:
    //   https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/javascript_s3_code_examples.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/classes/getobjectcommand.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/
    //
    /*
    look up assets bucket key in the database

    Call S3 to download the asset.
    To download an asset from S3 use Getobject command
*/


    const assetid = req.params.assetid;

    var rds_response = new Promise((resolve, reject) => {
      try {

        console.log("/download: calling RDS...");

        var sql = `
         select assetname,bucketkey,users.userid from assets 
         inner join users where assets.userid = users.userid and  assetid = ${assetid};
          `;

        dbConnection.query(sql, (err, results, _) => {
          try {
            if (err) {
              reject(err);
              return;
            }
            console.log("download query to get bucketkey is done");
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

    rds_result = await rds_response;

    if (rds_result.length === 0) {
      console.log("no asset found");
      res.status(400).json({
        "message": "no such asset...",
        "user_id": -1,
        "asset_name": "?",
        "bucket_key": "?",
        "data": []
      });
      return;
    }


    console.log("/download: calling S3...");

    async function downloadAsset() {
      const input = {
        Bucket: s3_bucket_name,
        Key: rds_result[0].bucketkey
      };

      const command = new GetObjectCommand(input);
      return s3.send(command)

    }

    const s3_response = await downloadAsset();
    var datastr = await s3_response.Body.transformToString("base64");


    Promise.all([datastr, rds_response]).then(results => {
      try {
        var s3_result = results[0];
        var rds_results = results[1];

        //Transform into base64-encoded string


        console.log("/downloads done, sending response...");

        res.json({
          "message": "success",
          "user_id": rds_results[0]["userid"],
          "asset_name": rds_results[0].assetname,
          "bucket_key": rds_results[0].bucketkey,
          "data": s3_result

        });
      }
      catch (code_err) {
        res.status(400).json({
          "message": code_err.message,
          "user_id": -1,
          "asset_name": "?",
          "bucket_key": "?",
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
        "user_id": -1,
        "asset_name": "?",
        "bucket_key": "?",
        "data": []
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
      "user_id": -1,
      "asset_name": "?",
      "bucket_key": "?",
      "data": []
    });
  }//catch

}//get
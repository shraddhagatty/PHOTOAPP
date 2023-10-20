//
// app.get('/bucket?startafter=bucketkey', async (req, res) => {...});
//
// Retrieves the contents of the S3 bucket and returns the 
// information about each asset to the client. Note that it
// returns 12 at a time, use startafter query parameter to pass
// the last bucketkey and get the next set of 12, and so on.
//
const { ListObjectsV2Command } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

exports.get_bucket = async (req, res) => {

  console.log("call to /bucket...");

  try {


    //
    // build input object with request parameters:
    //
    const startafter = req.query.startafter;
    var input = {
      Bucket: s3_bucket_name,
      MaxKeys: 12,
      SortBy: "Key",
      StartAfter: startafter
    };

    console.log("/bucket: calling S3...");

    var command = new ListObjectsV2Command(input);
    var s3_response = s3.send(command);

    Promise.all([s3_response]).then(results => {
      try {

        const s3_results = results[0].Contents

        console.log('/bucket done, sending response...')
        if (results[0].KeyCount === 0) {
          return res.json({
            "message": "success",
            "data": []
          });
        }

        res.json({
          "message": "success",
          "data": s3_results
        });

      }
      catch (code_err) {
        res.status(400).json({
          "message": code_err.message,
          "data": []

        });

      }
    });

  }//try
  catch (err) {
    res.status(400).json({
      "message": err.message,
      "data": []
    });
  }//catch

}//get

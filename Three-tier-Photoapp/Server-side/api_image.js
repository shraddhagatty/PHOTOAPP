//
// app.post('/image/:userid', async (req, res) => {...});
//
// Uploads an image to the bucket and updates the database,
// returning the asset id assigned to this image.
//
const dbConnection = require('./database.js')
const { PutObjectCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

const uuid = require('uuid');

exports.post_image = async (req, res) => {

  var userid = req.params.userid
  console.log("call to /image...");


  try {

    var rds_response = new Promise((resolve, reject) => {
      var sql = `
      select bucketfolder from users
      where userid=${userid}
      `
      dbConnection.query(sql, (err, results) => {
        if (err) {
          reject(err);
        } else {
          console.log("/query done");
  
          resolve(results);
        }
      });
  
    });
    const results = await rds_response;
    if (results == null) {
      res.json({
        "message":"no such user...",
        "assetid":-1
      })
      return;
    }
    const bucket = results.bucketfolder
    
    
	
	  var assetname = req.body.assetname
    var data = req.body.data;  // data => JS object
    console.log(data)
    var bytes = Buffer.from(data, 'base64');
    console.log(bytes)
      let name = uuid.v4()
      let key = bucket+'/'+name+".jpg"
      const command = new PutObjectCommand({
        Bucket: s3_bucket_name,
        Key: key,
        Body: bytes
      });
    

    const response = await s3.send(command);
    
    
    if (response.$metadata.httpStatusCode===200) {
      // console.log("upload success");
      try{
        var rds_response = new Promise((resolve, reject) => {
          var sql = `
          Insert into assets(userid, assetname, bucketkey)
          values (${userid}, "${assetname}", "${key}");
          `
          dbConnection.query(sql, (err, results) => {
            if (err) {
              reject(err);
            } else {
              // console.log("/query done");
              resolve(results);
              
            }
          });

        });
        const assetInsertResults = await rds_response;
        if (assetInsertResults){
          dbConnection.query('SELECT LAST_INSERT_ID() as id', (err, rows) => {
            if (err) {
              // Handle the error
              console.error(err);
            } else {
              lastInsertedID = rows[0].id;
              console.log('Last inserted ID:', lastInsertedID);
              res.json({
                "message":"success",
                "assetid":lastInsertedID
              })
            }
            });
          
        }
       
      }
      catch{
        console.log("error in inserting into assets")
      }
      
    }
    
    
    
    
	
  }//try
  catch (err) {
    console.log("**ERROR:", err.message);

    res.status(400).json({
      "message": err.message,
      "assetid": -1
    });
  }//catch

}//post

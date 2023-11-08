//
// app.put('/user', async (req, res) => {...});
//
// Inserts a new user into the database, or if the
// user already exists (based on email) then the
// user's data is updated (name and bucket folder).
// Returns the user's userid in the database.
//
const dbConnection = require('./database.js')

exports.put_user = async (req, res) => {

  console.log("call to /user...");

  try {

    var data = req.body;  // data => JS object
    
    console.log(data);
    var rds_response = new Promise((resolve, reject) => {
      var sql = `
      INSERT INTO users (email,lastname,firstname,bucketfolder)
      VALUES("${data.email}",
      "${data.lastname}",
      "${data.firstname}","${data.bucketfolder}")
      ON DUPLICATE KEY UPDATE lastname="${data.lastname}",
      firstname="${data.firstname}",
      bucketfolder="${data.bucketfolder}"
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
    const userId = results.insertId;
    const rowCount = results.affectedRows;

    // Determine if it was an insert or update
    const action = rowCount === 1 ? 'inserted' : rowCount === 2 ? 'updated' :               'No change';
    res.json({
      "message":action,
      "userid":userId
        
    })
	
	
	
  }//try
  catch (err) {
    console.log("**ERROR:", err.message);

    res.status(400).json({
      "message": "some sort of error message",
      "userid": -1
    });
  }//catch

}//put

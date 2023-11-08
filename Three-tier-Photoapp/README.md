# Three-Tier PhotoApp - A Cloud-Native Image Management Application

Welcome to the Three-Tier PhotoApp project. This cloud-native application allows users to manage their images through a server-side web service. This README will guide you through the project and its components.

## Project Overview

This project is divided into two parts: Project 01 and Project 02. Project 01 lays the foundation for the application by using AWS and Python for managing images. Project 02 introduces a server-side web service written in JavaScript using Node.js and the Express framework to provide a layer between the client and AWS services.

## Project Structure

The server-side web service consists of various files that provide the framework for the application. Below are the key files and their descriptions:

- **app.js:** The main file that listens on the proper port and registers the web service functions (API).
- **api_asset.js:** Handles assets related operations.
- **api_bucket.js:** Manages bucket-related functions.
- **api_download.js:** Facilitates image downloads.
- **api_stats.js:** Provides statistics related to the application.
- **api_users.js:** Manages user-related operations.
- **api_user.js:** Handles the insertion of new users into the database.
- **api_image.js:** Manages image uploading to Amazon S3.
- **aws.js:** Handles AWS-specific functionalities.
- **config.js:** Configuration settings for the web service.
- **database.js:** Manages database interactions.
- **photoapp-config.ini:** Configuration file for PhotoApp.

## API Functions

The web service defines several API functions for interacting with the application:

1. **/users :** This API function is used manage user operations.

2. **/image/:userid (POST):** This API function is responsible for uploading an image to Amazon S3 and storing information about the asset in the database. Each POST call creates a new image in S3, allowing for multiple uploads.

3. **/assets:** Manages operations related to assets.
4. **/bucket:** Handles operations related to the bucket.
5. **/download/:assetid:** Facilitates image downloads.
6. **/stats:** Provides statistics related to the application.
7. **/user (PUT):** This API function is used to insert a new user into the database or update existing user information based on the email address. Testing can be done using Postman.

## Deployment

To deploy your web service, you can use AWS Elastic Beanstalk to host it on an EC2 instance, making it accessible to the world.

## Getting Started

Follow these steps to get started with the Three-Tier PhotoApp:

1. Clone the repository from GitHub

2. Navigate to the "Project 02 (server)" directory or the provided location of the server-side files.

3. Set up your AWS credentials and configuration as needed.

4. Implement the API functions as described above.

5. Test your web service using tools like Postman.

6. Deploy your web service on AWS Elastic Beanstalk to make it accessible to users.

## Conclusion

The Three-Tier PhotoApp project enhances the functionality of the application by introducing a server-side web service. Users can now interact with the application through this web service, which provides a layer between the client and AWS services.



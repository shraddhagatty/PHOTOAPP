# PhotoApp - A Cloud-Native Image Management Application

This cloud-native application allows users to upload, download, and manipulate their images. In this project, we have implemented a two-tier architecture (Project 01) and a three-tier architecture (Project 02) using AWS, Python and Nodejs. This README will guide you through the key components and steps involved in both projects.

## Project 01 - Two-Tier PhotoApp

In Project 01, we built a client-server (two-tier) PhotoApp, where the client-side Python code directly interacted with AWS services. Here's what we accomplished:

1. **Storage with AWS S3**: We use Amazon S3 to store user images securely.

2. **Database with RDS**: We utilize RDS, specifically MySQL, to manage user data and image metadata.

3. **Access Control with IAM**: IAM is used to create users and policies for secure access to AWS services.

## Project 02 - Three-Tier PhotoApp

In Project 02, we introduce a web service tier between the Python-based client and AWS services. This tier is implemented in JavaScript using Node.js and the Express framework. The client remains Python-based but now interacts with the web service instead of AWS directly. The database and S3 bucket remain unchanged from Project 01.

Here are the major steps for Project 02:

1. **Build the Web Service**: Develop the web service using Node.js and Express. Test it locally in a web browser as the client.

2. **Python-Based Client**: Create a Python-based client that interacts with the web service, providing a more convenient way to test.

3. **Image Upload**: Add image upload functionality to the web service, update the Python client, and ensure proper testing.

4. **Deployment**: Package and deploy the application using AWS Elastic Beanstalk or EC2, making it accessible to users worldwide.

## Getting Started

To get started with this project, follow these steps:

1. Clone this repository to your local machine.

2. Review the documentation for each project located in the respective directories:
   - Project 01: [Two-Tier PhotoApp](Two-tier-Photoapp/README.md)
   - Project 02: [Three-Tier PhotoApp](Three-tier-Photoapp/README.md)

3. Follow the instructions in the documentation to set up and run the projects.

This project was developed during the Indigenous Australian Datathon 2023. It is not a completed project, merely a reference to the work achieved during this session. 
Also note, this is not an official AWS project. It is a project built using AWS, by a varied team of attendees

# How to Setup
## [Maxus AI](https://www.maxusai.com/)
1. Register an account and setup a project
2. Upload your training dataset (200-250 images of the object you want to detect) into an S3 bucket with access or local hard drive
3. Complete the identification of the object in all the images in the training set
4. Train the model

## Lambda Functions
### Maxus AI Endpoint
1. Set up an S3 bucket to upload your objects
2. Create a lambda function with a trigger from this S3 on any upload
3. Ensure you have the relevant information to reach the MaxusAI endpoint
    API_KEY
    MODEL_ID
    PROJECT_ID
4. Set these values in the configuration setting of your lambda as Environment Variables
5. Run the following in the relevant lambda file to compress and zip your function
    ``
6. Upload to the lambda
7. Ensure your permissions are correct to access the bucket
8. This function takes longer than 3 seconds to run. You will need to expand that time.
9. Test an upload
10. Set the destination to be an SNS topic that triggers on success

### Convert AI Output to Human Readable
1. Create the lambda and copy and paste the relevant code in this repo into the lambda
2. Subscribe lambda to above SNS topic. Ensure it appears as the trigger
3. Test the function

# Future Steps
- take the human readable output and use it to create automations
    email/sms rangers about number of pigs detected
    create dashboards
    traps

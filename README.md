# StreamingDataProject
This tool retrieves up to 10 articles from The Guardian API based on a search term and optional date filter, then publishes them to an AWS Kinesis stream in JSON format.


## About
- Search the Guardian API for specified articles 
- Fitler by date and search term 
- Publish these articles to AWS Kenisis
- Includes a content preview which displays first 1000 characters of article 
- Command line interface for improved user experience

## Installation guide
- Clone this repository
- Install the dependencies e.g pip install -r requirements.txt
- Create a `.env` file in the project root directory: GUARDIAN_API_KEY=your_guardian_api_key_here
- When using AWS cli enter `aws configure`
- Environment variables required: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

## API keys
- Go to: https://open-platform.theguardian.com/access/
- Register for a free API key
- Add this key to .env file

## Testing on local machine using kinesalite
You can use kinesalite (Installed with node) and run on your local machine, from there you can provide the url under the .env AS LOCAL_KINESIS_ENDPOINT_URL

EG run kinesalite --port 4567 and set LOCAL_KINESIS_ENDPOINT_URL=http://localhost:4567 

If you want to read the stream for development purpsoes, you can use ./read_kinesis_stream.py "STREAM_NAME" 
and replace STREAM_NAME with the actual name of the stream inputted

## How to use AWS
- Create an AWS Kinesis stream using the cli, e.g. `aws kinesis create-stream --stream-name my_kinesis_stream --shard-count 1`
- configure the rate of retention for the data: (should be removed by three days according to requirements)
e.g. aws kinesis increase-stream-retention-period --stream-name my_kinesis_stream --retention-period-hours 72

 

# lambda-epubify

[![License](https://img.shields.io/dub/l/vibe-d.svg)](http://doge.mit-license.org)

`epubify` is a Python program that creates an ePUB ebook from a list of URLs. `lambda-epubify` is a project to run `epubify` on AWS Lambda.

# Build

To run this project on Lambda, you'll need to build it first on Amazon Linux. *In the future, a release will be provided with a pre-built ZIP file ready to upload to Lambda.*

1. Provision an EC2 instance running Amazon Linux. The instance needs at least 1GB of RAM in order to compile lxml, so a t2.nano instance cannot be used to build this project.
2. Install `git`: `sudo yum update && sudo yum install -y git`
3. Clone this repository: `git clone https://github.com/scascketta/lambda-epubify.git`
4. Install lxml's dependencies by running the `bootstrap.sh` script.
5. Run the `build.sh` script to build a ZIP file.

The ZIP file created on step 4 is ready to be uploaded to AWS Lambda and invoked.

# Usage

`lambda-epubify` essentially takes a list of URLs, turns them into an ebook, and then saves that ebook into an S3 bucket.

Specifically, it expects a payload that looks like this:

```
{
  "output": {
    "key": "<s3-key>", // the full S3 key for the created ePUB file (e.g. 'epubify-test.epub')
    "bucket": "<your-s3-bucket>" // the S3 bucket to place the ePub file in
  },
  "title": "<your-title>",
  "urls": [
    "<url-1>"
    ...
    "<url-N>"
  ]
}
```

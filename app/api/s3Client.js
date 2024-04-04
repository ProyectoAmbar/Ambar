import AWS from 'aws-sdk';

AWS.config.update({
  region: 'US-central',
  accessKeyId: '5b14f3d5b717570e7fa33c2f66f5bac5',
  secretAccessKey: 'aeaa5dc280a76d634767cece24d14962',
});

const S3Client = new AWS.S3({
  endpoint: 'https://usc1.contabostorage.com', 
  s3ForcePathStyle: true, 
  signatureVersion: 'v4'
});

export default S3Client;

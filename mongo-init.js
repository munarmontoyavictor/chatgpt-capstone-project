db = db.getSiblingDB('chatgpt_mongodb');
db.createCollection('transcriptions');
db.createUser({
  user: 'vamunarm',
  pwd: 'chatgpt',
  roles: [{ role: 'readWrite', db: 'chatgpt_mongodb' }],
});


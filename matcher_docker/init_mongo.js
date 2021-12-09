db = db.getSiblingDB('admin');
db.createUser({
    'user': _getEnv('MONGO_ADMIN_USERNAME'),
    'pwd': _getEnv('MONGO_ADMIN_PASSWORD'),
    'roles': ['root']
});

db = db.getSiblingDB(_getEnv('MONGO_DATABASE'));
db.createUser({
    'user': _getEnv('MONGO_USERNAME'),
    'pwd': _getEnv('MONGO_PASSWORD'),
    'roles': ['readWrite']
});

db.createCollection('userData');
db.getCollection('userData').createIndex({'userId': 1}, {'unique': true})

db.createCollection('userPreference');
db.getCollection('userPreference').createIndex({'userId': 1}, {'unique': true})

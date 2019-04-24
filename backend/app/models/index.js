var fs = require('fs');
var path = require('path');
var basename = path.basename(__filename);
var models = {};
const mongoose = require('mongoose');

if (CONFIG.db_host != '') {
    var files = fs
        .readdirSync(__dirname)
        .filter((file) => {
            return (file.indexOf('.') !== 0) && (file !== basename) && (file.slice(-3) === '.js');
        })
        .forEach((file) => {
            var filename = file.split('.')[0];
            var model_name = filename.charAt(0).toUpperCase() + filename.slice(1);
            models[model_name] = require('./' + file);
        });

    mongoose.Promise = global.Promise; //set mongo up to use promises
    const mongo_location = CONFIG.mongo_uri
    //'mongodb://' + CONFIG.db_user +":"+ CONFIG.db_password  + '@' + CONFIG.db_ip + ':' + CONFIG.db_port + '/' + CONFIG.db_name;
    
    mongoose.connect(mongo_location, { useNewUrlParser: true });

    let db = mongoose.connection;
    module.exports = db;
    db.once('open', () => {
        console.log('Connected to mongo at ' + mongo_location);
    })
    db.on('error', (error) => {
        console.log("error", error);
    })
    // End of Mongoose Setup
} else {
    console.log("No Mongo Credentials Given");
}

module.exports = models;
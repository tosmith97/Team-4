require('./config/config'); //instantiate configuration variables
require('./config/keys'); // instantiate authorization variables
require('./global_functions'); //instantiate global functions


console.log("Environment:", CONFIG.app)

const express = require('express');
const logger = require('morgan');
const bodyParser = require('body-parser');
const expressValidator = require('express-validator');
const cookieParser = require('cookie-parser');
const mongoose = require('mongoose');

const v1 = require('./app/routes/v1');

const app = express();

app.use(logger('dev'));
app.use(cookieParser());
app.use(bodyParser.json({limit: '10mb'}));
app.use(bodyParser.urlencoded({
	extended: false
}));
app.use(expressValidator()); // this line must be immediately after any of the bodyParser middlewares!

//DATABASE
const models = require("./app/models");

// CORS
app.use(function (req, res, next) {
	// Website you wish to allow to connect
	res.setHeader('Access-Control-Allow-Origin', '*');
	// Request methods you wish to allow
	res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
	// Request headers you wish to allow
	res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With, content-type, Authorization, Content-Type, origin');
	// Set to true if you need the website to include cookies in the requests sent
	// to the API (e.g. in case you use sessions)
	res.setHeader('Access-Control-Allow-Credentials', true);
	// Pass to next layer of middleware
	next();
});

app.use('/v1', v1);

app.use('/', function (req, res) {
	res.statusCode = 200; //send the appropriate status code
	res.json({
		status: "success",
		message: "Parcel Pending API",
		data: {}
	})
});

// catch 404 and forward to error handler
app.use(function (req, res, next) {
	var err = new Error('Not Found');
	err.status = 404;
	next(err);
});

// error handler
app.use(function (err, req, res, next) {
	// set locals, only providing error in development
	res.locals.message = err.message;
	res.locals.error = req.app.get('env') === 'development' ? err : {};

	// render the error page
	res.status(err.status || 500);
	res.json({error: err.message});
});

// disconnect from mongoose on app shutdown
const gracefulShutdown = async function (msg, callback) {
	await mongoose.connection.close(function () {
	    console.log('Mongoose disconnected through ' + msg);
	    callback();
	});
};
process.once('SIGUSR2', async function () {
	await gracefulShutdown('nodemon restart', async function () {
	    await process.kill(process.pid, 'SIGUSR2');
	});
});
// For app termination
process.on('SIGINT', async function() {
	await gracefulShutdown('app termination', function () {
	    process.exit(0);
	});
});
process.on('SIGTERM', async function() {
	await gracefulShutdown('AWS app termination', function () {
	    process.exit(0);

	});
});

module.exports = app;

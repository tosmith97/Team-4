const mongoose = require('mongoose');

// define the schema for our user model
let UserSchema = mongoose.Schema({
    name: {
        type: String
    },
    email: {
        type: String,
        unique: true,
        required: [true, "This field can't be blank"],
        match: [/\S+@\S+\.\S+/, 'is invalid'],
        index: true,
        trim: true,
    },
    reports: [{
        _id: false,
        reporter: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "User"
        },
        timeReported: {
            type: Date,
            default: Date.now
        },
    }]
}, {
    timestamps: true
});

const User = module.exports = mongoose.model('User', UserSchema);

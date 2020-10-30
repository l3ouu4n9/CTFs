const qs = require('qs');
const express = require('express');
const bodyParser = require('body-parser');
const expressLayouts = require('express-ejs-layouts');
const validateAuthentication = require('./lib/auth').validate;

// Express
const app = express();
app.use(expressLayouts);
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({
    extended: true,
    verify: (req, res, buf, encoding) => {
        const rawBody = buf.toString(encoding || 'utf-8');

        // Security fix
        req.data = {};
        try {
            req.data = qs.parse(rawBody, {
                allowPrototypes: false,
            });
        } catch (error) {
            console.log(error);
        }
    }
}));


// Login Page
app.get('/', (req, res, next) => {
    res.redirect('/login');
});


// Login Page
app.get('/login', (req, res, next) => {
    res.render('login', {error: ""});
});

// Login
app.post('/login', (req, res) => {
    class User {
        constructor(name, pass, role = "guest") {
            this.name = name;
            this.password = pass;
            this.role = role;
        }
    }

    User.prototype.toString = function () {
        return `[${this.role}] ${this.name}`;
    }

    const remoteIP = "1.3.3.7";
    const user = new User();
    for (let [key, value] of Object.entries(req.data)) {
        user[key] = value
    }

    // Regular User Check (No Injections Here! ;)
    const error = validateAuthentication(user);
    if (error) {
        return res.render('login', {
            error: error
        });
    }

    // It looks unstable
    try {
        // Log users
        console.log(`User: \{ ${user} \}`);

        // Under Construction For Guests
        if (user.role !== "admin") {
            return res.render('login', {
                error: "Under construction, please wait few more day..."
            });
        }

        if (user.role === "admin" && remoteIP !== "127.0.0.1") {
            return res.render('login', {
                error: "You Cannot Login As Admin From Here!"
            });
        }
    } catch (error) {
        console.log(error);
    }

    return res.render('flag', {
        flag: process.env.FLAG
    })

});


const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`)
});

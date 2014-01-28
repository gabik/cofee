// Array remove function
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};

//var app = require('express').createServer();
var fs = require('fs');
var express = require("express");
var app = express();
var io = require('socket.io').listen(app.listen(8889));
var $ = require('jquery');



// routing
app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

app.get('/orders.css', function (req, res) {
  res.sendfile(__dirname + '/orders.css');
});

app.get('/menu.css', function (req, res) {
  res.sendfile(__dirname + '/menu.css');
});

app.get('/admin', function (req, res) {
  res.sendfile(__dirname + '/admin.html');
});

// branches which are currently connected to the system
var branches = {};

io.sockets.on('connection', function (socket) {

	// on new connection of branch client
	socket.on('connectBranch', function(branchID) {
		//save ID info on the socket
		socket.branchID = branchID
		// save the socket of the branch by ID
		var branchSocketsArray=new Array();
		if(branchID in branches) {
			branchSocketsArray=branches[branchID];
		}
		branchSocketsArray.push(socket);
		branches[branchID]=branchSocketsArray;
		console.log("CURRENT BRANCHES: " + branches[branchID]);
		// ask the client to run getAllObjects function with orders JSON
		for (var i = 0; i < branchSocketsArray.length; i++) {
			branchSocketsArray[i].emit('getAllOrders');
		}
	});

	// check if branch is online
	socket.on('checkOnline', function(branchID) {
		var json = {};
		for (var k in branches) {
			json[k] = k;
			console.log(branches[k].length);
		}
		
		socket.emit('onlineStatus', json);
	});
	// clear - for test
	socket.on('clearOrders', function(branchID) {
		if (branchID in branches) {
			var branchSocketsArray = branches[branchID];
			for (var i = 0; i < branchSocketsArray.length; i++) {
				branchSocketsArray[i].emit('clearOrders');
			}
		}
	});
	
	// when the client change order he tells the server and we will send him update json
	socket.on('updateOrder', function (branchID, oid, ostatus) {
		// we tell the client to execute 'changeOrder' with json
		var error_flag=0;
		var error_msg="";
		if (branchID in branches) {
			tmp_filename = Math.random().toString(36).substring(8);
			tmp_hash = Math.random().toString(36).substring(2);
			fs.writeFile("./static/tmp/"+tmp_filename, tmp_hash, function(err) {
				if(err) {
					error_flag=1;
					error_msg=err;
				} else {
					var json;
					var branchSocketsArray = branches[branchID];
					if (ostatus == "dodone") {
						json = {id:oid};
						for (var i = 0; i < branchSocketsArray.length; i++) {
							branchSocketsArray[i].emit('deleteOrder', json);
						}
					} else {
						var ost;
						if (ostatus == "doready") {
							ost = "ready";
						} else if (ostatus == "dononready") {
							ost = "nonready";
						} else {
							ost = "error";
						}
						json = {id:oid,status:ost};
						for (var i = 0; i < branchSocketsArray.length; i++) {
							branchSocketsArray[i].emit('changeOrder', json);
						}
					}
				}
			}); 
		} else {
			error_flag = 1;
			error_msg = "Branch ID looks like disconnected... try to refresh your browser.";
		}
		
		if (error_flag == 1) {
			socket.emit('raiseError', error_msg);
			console.log("Error... FILE: " + tmp_filename);
		}
	});

	// when the client emits 'addOrder', this listens and executes
	socket.on('addOrder', function(branchID, orderID){
		if (branchID in branches) {
			var branchSocketsArray = branches[branchID];
			for (var i = 0; i < branchSocketsArray.length; i++) {
				branchSocketsArray[i].emit('addOrder', orderID);
			}
		}
	});

	// when the user disconnects.. perform this
	socket.on('disconnect', function(){
		// remove the branch from global branches list
		if (socket.branchID in branches) {
			var branchSocketsArray = branches[socket.branchID];
			if ( branchSocketsArray.length == 1 ) {
				delete branches[socket.branchID];
			} else {
				for (var i = 0; i < branchSocketsArray.length; i++) {
					if (branchSocketsArray[i] == socket) {
						branches[socket.branchID].remove(i);
						console.log("DROPPING 1 CLIENT!!");
					}
				}
			}
		}
		// update DB that the branch is offline
	});
});


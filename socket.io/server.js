//for test-build JSON for first login
ordersJson = {"count":6,"orders":[{"id":345,"state":"nonready"},{"id":346,"state":"ready"},{"id":545,"state":"nonready"},{"id":645,"state":"nonready"},{"id":745,"state":"ready"},{"id":845,"state":"nonready"}]};

var app = require('express').createServer()
var io = require('socket.io').listen(app.listen(8888));


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

app.post('/new_order', function(req, res) {
  console.log(req);
});

// branches which are currently connected to the system
var branches = {};

io.sockets.on('connection', function (socket) {

	// on new connection of branch client
	socket.on('connectBranch', function(branchID) {
		//save ID info on the socket
		socket.branchID = branchID
		// save the socket of the branch by ID
		branches[branchID]=socket;
		// ask the client to run getAllObjects function with orders JSON
		branches[branchID].emit('getAllOrders', ordersJson);
	});

	// clear - for test
	socket.on('clearOrders', function(branchID) {
		branches[branchID].emit('clearOrders');
	});
	
	// when the client change order he tells the server and we will send him update json
	socket.on('updateOrder', function (oid, ostatus) {
		// we tell the client to execute 'changeOrder' with json
		var json;
		if (ostatus == "dodone") {
			json = {id:oid};
			io.sockets.emit('deleteOrder', json);
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
			io.sockets.emit('changeOrder', json);
		}
	});

	// when the client emits 'addOrder', this listens and executes
	socket.on('addOrder', function(branchID, orderID){
		branches[branchID].emit('addOrder', orderID);
	});

	// when the user disconnects.. perform this
	socket.on('disconnect', function(){
		// remove the branch from global branches list
		delete branches[socket.branchID];
		// update DB that the branch is offline
	});
});


const express = require("express");  // Express for handling routes
const cors = require("cors");  // Allow frontend to call backend
require("dotenv").config(); // For environment variables

const app = express();
app.use(express.json()); // To handle JSON requests
app.use(cors()); // Allow frontend requests

// Simple API route for testing
app.get("/", (req, res) => {
    res.send("Server is running!");
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

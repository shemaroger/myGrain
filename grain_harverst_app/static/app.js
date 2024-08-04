// const locationButton = document.querySelector('.location-button');
// const chatMessages = document.querySelector('.chat-messages');
// const chatInputForm = document.querySelector('.chat-input-form');
// const chatInput = document.querySelector('.chat-input');
// const clearChatBtn = document.querySelector('.clear-chat-button');
// const johnSelectorBtn = document.querySelector('#john-selector');
// // const janeSelectorBtn = document.querySelector('#jane-selector'); // Uncomment if you have another user

// const chatHeader = document.querySelector('.chat-header');

// // Retrieve messages from localStorage or initialize an empty array
// let messages = JSON.parse(localStorage.getItem('messages')) || [];

// // Function to create HTML structure for a chat message
// const createChatMessageElement = (message) => `
//   <div class="message ${message.sender === 'Distributor' ? 'blue-bg' : 'gray-bg'}">
//     <div class="message-sender">${message.sender}</div>
//     <div class="message-text">${message.text}</div>
//     <div class="message-timestamp">${message.timestamp}</div>
//   </div>
// `;

// // Function to update the sender of messages
// let messageSender = 'Distributor'; // Default sender is John

// const updateMessageSender = (name) => {
//   messageSender = name;
//   chatHeader.innerText = `${messageSender} chatting...`;
//   chatInput.placeholder = `Type here, ${messageSender}...`;

//   // Update active class based on selected sender
//   if (name === 'Distributor') {
//     johnSelectorBtn.classList.add('active-person');
//     // janeSelectorBtn.classList.remove('active-person'); // Uncomment if you have another user
//   }
//   // else if (name === 'Farmer') {
//   //   janeSelectorBtn.classList.add('active-person');
//   //   johnSelectorBtn.classList.remove('active-person');
//   // }

//   // Auto-focus the input field after updating sender
//   chatInput.focus();
// };

// // Event listeners for sender selection buttons
// johnSelectorBtn.addEventListener('click', () => updateMessageSender('Distributor'));
// // janeSelectorBtn.addEventListener('click', () => updateMessageSender('Farmer')); // Uncomment if you have another user

// // Function to handle sharing location
// const shareLocation = () => {
//   if (!navigator.geolocation) {
//     alert('Geolocation is not supported by your browser');
//     return;
//   }

//   // Disable the button during the request
//   locationButton.disabled = true;

//   // Retrieve current geolocation coordinates
//   navigator.geolocation.getCurrentPosition(
//     (position) => {
//       const { latitude, longitude } = position.coords;
//       const locationMessage = `Latitude: ${latitude}, Longitude: ${longitude}`;

//       // Construct message object with location data
//       const timestamp = new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
//       const message = {
//         sender: messageSender,
//         text: locationMessage,
//         timestamp,
//         location: { latitude, longitude }
//       };

//       // Log message to console
//       console.log('Message sent:', message);

//       // Save message to local storage
//       messages.push(message);
//       localStorage.setItem('messages', JSON.stringify(messages));

//       // Add message to DOM
//       appendMessageToChat(message);

//       // Clear input field and re-enable location button
//       chatInputForm.reset();
//       locationButton.disabled = false;

//       // Scroll to bottom of chat messages
//       chatMessages.scrollTop = chatMessages.scrollHeight;
//     },
//     (error) => {
//       alert(`Unable to retrieve your location: ${error.message}`);
//       locationButton.disabled = false;
//     }
//   );
// };

// // Event listener for clicking the location share button
// locationButton.addEventListener('click', shareLocation);

// // Function to handle sending a regular text message
// const sendMessage = (e) => {
//   e.preventDefault();

//   // Retrieve current timestamp
//   const timestamp = new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });

//   // Construct message object
//   const message = {
//     sender: messageSender,
//     text: chatInput.value,
//     timestamp,
//   };

//   // Log message to console
//   console.log('Message sent:', message);

//   // Save message to local storage
//   messages.push(message);
//   localStorage.setItem('messages', JSON.stringify(messages));

//   // Add message to DOM
//   appendMessageToChat(message);

//   // Clear input field
//   chatInput.value = '';

//   // Scroll to bottom of chat messages
//   chatMessages.scrollTop = chatMessages.scrollHeight;
// };

// // Event listener for submitting the chat input form
// chatInputForm.addEventListener('submit', sendMessage);

// // Function to append a message to the chat messages container
// const appendMessageToChat = (message) => {
//   const messageElement = createChatMessageElement(message);
//   chatMessages.innerHTML += messageElement;
// };

// // Function to clear the chat messages and local storage
// const clearChat = () => {
//   localStorage.removeItem('messages');
//   messages = []; // Clear messages array
//   chatMessages.innerHTML = ''; // Clear chat messages
// };

// // Event listener for clearing the chat
// clearChatBtn.addEventListener('click', clearChat);

// // Initial setup: Display existing messages from localStorage
// const displayMessages = () => {
//   chatMessages.innerHTML = ''; // Clear existing messages

//   messages.forEach(message => {
//     appendMessageToChat(message);
//   });

//   // Scroll to bottom of chat messages
//   chatMessages.scrollTop = chatMessages.scrollHeight;
// };

// // Call displayMessages on page load
// displayMessages();

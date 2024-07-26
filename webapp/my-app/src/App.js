import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileInputKey, setFileInputKey] = useState(Date.now());

  useEffect(() => {
    // Fetch messages from the Flask API
    axios.get('http://127.0.0.1:5000/api/messages')
      .then(response => {
        setMessages(response.data);
      })
      .catch(error => {
        console.error('Error fetching messages:', error);
      });
  }, []);

  const handleSendMessage = () => {
    if (newMessage.trim() === '') return;

    const userMessage = { text: newMessage, sender: 'user' };

    // Send new message to the Flask API
    axios.post('http://127.0.0.1:5000/api/messages', userMessage)
      .then(response => {
        const llmMessage = response.data;
        setMessages(prevMessages => [...prevMessages, userMessage, llmMessage]);
        setNewMessage('');  // Clear the input field
      })
      .catch(error => {
        console.error('Error sending message:', error);
      });
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSendMessage();
    }
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUploadImage = () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('text', newMessage);  // Append the text message

    axios.post('http://127.0.0.1:5000/api/upload', formData)
      .then(response => {
        const llmMessage = response.data;
        setMessages(prevMessages => [...prevMessages, llmMessage]);
        setSelectedFile(null);  // Clear the selected file
        setNewMessage('');  // Clear the input field
        setFileInputKey(Date.now());  // Reset the file input key to force re-render
      })
      .catch(error => {
        console.error('Error uploading image:', error);
      });
  };

  return (
    <div className="chat-container">
      <div className="chat-header">Chat with LLM</div>
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}  // Unique key for each message
            className={`chat-message ${message.sender}`}
          >
            <b>{message.sender === 'user' ? 'You' : 'LLM'}:</b> {message.text}
          </div>
        ))}
      </div>
      <div className="chat-input-container">
        <input
          type="text"
          className="chat-input"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={handleKeyPress}  // Add keypress event listener
          placeholder="Type your message..."
        />
        <button onClick={handleSendMessage} className="chat-button">Send</button>
      </div>
      <div className="chat-input-container">
        <input key={fileInputKey} type="file" onChange={handleFileChange} />
        <button onClick={handleUploadImage} className="chat-button">Upload Image</button>
      </div>
    </div>
  );
};

export default App;





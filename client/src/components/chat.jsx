// src/Chat.js
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./chat.css";

const Chat = () => {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("nlp");

  const chatEndRef = useRef(null);

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    const newMessages = [...messages, { type: "user", text: question }];
    setMessages(newMessages);

    // To work in render
    const backendUrl = "https://chatbotbackend-aqoc.onrender.com"; // Use your Render backend URL

    const url =
      mode === "nlp" ? `${backendUrl}/nlp-query` : `${backendUrl}/rag-query`;

    // To work in local

    //const url =
    //mode === "nlp"
    //? "http://127.0.0.1:8000/nlp-query"
    //: "http://127.0.0.1:8000/rag-query";

    try {
      const res = await axios.post(
        url,
        { question: question },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log(res);
      setMessages((prev) => [
        ...newMessages,
        { type: "bot", text: res.data.response },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...newMessages,
        { type: "bot", text: "Sorry, I couldn't understand that." },
      ]);
    }

    setQuestion(""); // Clear the question field
    setLoading(false);
  };

  // Scroll to the bottom when messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Function to toggle between NLP and RAG modes
  const toggleMode = () => {
    setMode((prevMode) => (prevMode === "nlp" ? "rag" : "nlp"));
  };

  return (
    <div className="chat-container">
      <h1 className="chat-title">Arol Chatbot</h1>
      <div className="chat-box">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type}`}>
            {message.text}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <form className="input-area" onSubmit={handleSubmit}>
        <div className="switch-container">
          <label className="switch">
            <input type="checkbox" onChange={toggleMode} />
            <span className="slider round"></span>
          </label>
          <span className="mode-label">{mode === "nlp" ? "NLP" : "RAG"}</span>
        </div>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your message..."
          rows="1"
        />
        <button className="send-button" type="submit" disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </form>
    </div>
  );
};

export default Chat;

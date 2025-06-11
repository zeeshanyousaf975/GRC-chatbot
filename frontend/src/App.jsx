import React from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Navigation Chatbot</h1>
        <p>Ask me how to navigate the software platform</p>
      </header>
      <main className="App-main">
        <ChatInterface />
      </main>
      <footer className="App-footer">
        <p>Powered by LangChain, Neo4j, and GROQ LLM</p>
      </footer>
    </div>
  );
}

export default App; 
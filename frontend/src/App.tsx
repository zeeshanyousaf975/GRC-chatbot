import React from 'react';
import ChatWindow from './components/ChatWindow';
import './styles/App.css';

function App() {
  return (
    <div className="app-fullscreen">
      <header className="app-header">
        <h1>Chat Agent</h1>
        <p>Powered by Autogen and Groq LLM</p>
      </header>
      <main className="app-main-fullscreen">
        <ChatWindow />
      </main>
      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} - Chat Agent</p>
      </footer>
    </div>
  );
}

export default App; 
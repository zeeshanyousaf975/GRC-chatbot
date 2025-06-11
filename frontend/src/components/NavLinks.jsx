import React from 'react';
import './NavLinks.css';

const NavLinks = ({ sources, onLinkSelect }) => {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div className="nav-links-container">
      <h3>Suggested Navigation Links</h3>
      <div className="nav-links">
        {sources.map((source, index) => (
          <button
            key={index}
            className="nav-link"
            onClick={() => onLinkSelect(source.url)}
          >
            {source.title}
          </button>
        ))}
      </div>
    </div>
  );
};

export default NavLinks; 
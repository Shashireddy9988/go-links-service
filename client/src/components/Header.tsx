import React from 'react';
import { Link2, Plus } from 'lucide-react';

interface HeaderProps {
  onOpenCreateModal: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onOpenCreateModal }) => {
  return (
    <header className="header">
      <div className="logo-group">
        <div className="logo-icon">
          <Link2 size={24} color="#ffffff" />
        </div>
        <div className="logo-text">
          <h1>Go Links</h1>
          <p>Internal URL Shortener & Directory</p>
        </div>
      </div>
      <button className="btn-primary" onClick={onOpenCreateModal}>
        <Plus size={18} />
        New Shortcut
      </button>
    </header>
  );
};

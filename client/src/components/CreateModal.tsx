import React, { useState } from 'react';
import { X, Link, Globe, FileText, Tag as TagIcon } from 'lucide-react';
import { CreateGoLinkDTO } from '../types';

interface CreateModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (dto: CreateGoLinkDTO) => Promise<void>;
}

export const CreateModal: React.FC<CreateModalProps> = ({ isOpen, onClose, onSubmit }) => {
  const [alias, setAlias] = useState('');
  const [targetUrl, setTargetUrl] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [tagsInput, setTagsInput] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!alias.trim() || !targetUrl.trim() || !title.trim()) {
      setError('Alias, Target URL, and Title are required');
      return;
    }

    const tags = tagsInput
      .split(',')
      .map((t) => t.trim())
      .filter((t) => t.length > 0);

    setLoading(true);
    try {
      await onSubmit({
        alias: alias.trim(),
        targetUrl: targetUrl.trim(),
        title: title.trim(),
        description: description.trim() || undefined,
        tags,
      });

      // Reset form on success
      setAlias('');
      setTargetUrl('');
      setTitle('');
      setDescription('');
      setTagsInput('');
      onClose();
    } catch (err: any) {
      setError(err.message || 'An error occurred while creating the link');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create New Shortcut</h2>
          <button className="btn-icon" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        {error && (
          <div style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#f87171', padding: '0.75rem 1rem', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.875rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Shortcut Alias</label>
            <div className="alias-input-wrapper">
              <span className="alias-prefix">go/</span>
              <input
                type="text"
                placeholder="design-system"
                value={alias}
                onChange={(e) => setAlias(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Target URL</label>
            <input
              type="url"
              placeholder="https://figma.com/file/..."
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Title</label>
            <input
              type="text"
              placeholder="Design System & Component Library"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Description (Optional)</label>
            <textarea
              rows={3}
              placeholder="Brief summary of what this resource contains..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Tags (Comma separated)</label>
            <input
              type="text"
              placeholder="design, ui, frontend"
              value={tagsInput}
              onChange={(e) => setTagsInput(e.target.value)}
            />
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creating...' : 'Create Shortcut'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

import React from 'react';
import { GoLink } from '../types';
import { Copy, ExternalLink, Trash2, MousePointerClick, Check } from 'lucide-react';

interface LinkCardProps {
  link: GoLink;
  onDelete: (id: string) => void;
  onCopy: (text: string) => void;
  copiedId: string | null;
}

export const LinkCard: React.FC<LinkCardProps> = ({ link, onDelete, onCopy, copiedId }) => {
  const isCopied = copiedId === link.id;
  const shortcutUrl = `${window.location.origin}/go/${link.alias}`;

  return (
    <div className="link-card">
      <div>
        <div className="link-header">
          <span className="alias-tag">
            go/{link.alias}
          </span>
          <div className="actions-group">
            <button
              className="btn-icon"
              title="Copy Go Link"
              onClick={() => onCopy(shortcutUrl)}
            >
              {isCopied ? <Check size={16} color="#10b981" /> : <Copy size={16} />}
            </button>
            <a
              href={`/go/${link.alias}`}
              target="_blank"
              rel="noreferrer"
              className="btn-icon"
              title="Open Target URL (Redirects & counts click)"
            >
              <ExternalLink size={16} />
            </a>
            <button
              className="btn-icon delete"
              title="Delete Shortcut"
              onClick={() => onDelete(link.id)}
            >
              <Trash2 size={16} />
            </button>
          </div>
        </div>

        <h3 className="link-title">{link.title}</h3>
        {link.description && <p className="link-desc">{link.description}</p>}

        <div className="target-url-preview" title={link.targetUrl}>
          <ExternalLink size={12} />
          {link.targetUrl}
        </div>

        {link.tags.length > 0 && (
          <div className="tags-list">
            {link.tags.map((tag) => (
              <span key={tag} className="tag-pill">
                #{tag}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="link-footer">
        <span className="click-badge">
          <MousePointerClick size={14} />
          {link.clickCount} clicks
        </span>
        <span>
          Created {new Date(link.createdAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
        </span>
      </div>
    </div>
  );
};

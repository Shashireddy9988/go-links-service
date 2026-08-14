import React from 'react';
import { GoLink } from '../types';
import { Link, MousePointerClick, Tag, Award } from 'lucide-react';

interface StatsOverviewProps {
  links: GoLink[];
}

export const StatsOverview: React.FC<StatsOverviewProps> = ({ links }) => {
  const totalLinks = links.length;
  const totalClicks = links.reduce((sum, link) => sum + link.clickCount, 0);

  const uniqueTags = new Set(links.flatMap((l) => l.tags)).size;

  const topLink = links.length > 0 ? [...links].sort((a, b) => b.clickCount - a.clickCount)[0] : null;

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-icon">
          <Link size={24} />
        </div>
        <div className="stat-info">
          <div className="stat-value">{totalLinks}</div>
          <div className="stat-label">Active Shortcuts</div>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon" style={{ color: '#10b981' }}>
          <MousePointerClick size={24} />
        </div>
        <div className="stat-info">
          <div className="stat-value">{totalClicks}</div>
          <div className="stat-label">Total Redirects</div>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon" style={{ color: '#a855f7' }}>
          <Tag size={24} />
        </div>
        <div className="stat-info">
          <div className="stat-value">{uniqueTags}</div>
          <div className="stat-label">Categories / Tags</div>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon" style={{ color: '#f59e0b' }}>
          <Award size={24} />
        </div>
        <div className="stat-info">
          <div className="stat-value" style={{ fontSize: '1.25rem', fontFamily: 'var(--font-mono)' }}>
            {topLink ? `go/${topLink.alias}` : 'N/A'}
          </div>
          <div className="stat-label">Most Visited Link ({topLink ? topLink.clickCount : 0} clicks)</div>
        </div>
      </div>
    </div>
  );
};

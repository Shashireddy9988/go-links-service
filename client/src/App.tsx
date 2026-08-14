import React, { useEffect, useState } from 'react';
import { GoLink, CreateGoLinkDTO } from './types';
import { fetchLinks, createLink, deleteLink } from './services/api';
import { Header } from './components/Header';
import { StatsOverview } from './components/StatsOverview';
import { LinkCard } from './components/LinkCard';
import { CreateModal } from './components/CreateModal';
import { Search, ArrowUpDown, Check } from 'lucide-react';

export const App: React.FC = () => {
  const [links, setLinks] = useState<GoLink[]>([]);
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState<'createdAt' | 'clickCount' | 'alias'>('createdAt');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadLinks = async () => {
    try {
      setLoading(true);
      const data = await fetchLinks(search, undefined, sortBy);
      setLinks(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLinks();
  }, [search, sortBy]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  const handleCreate = async (dto: CreateGoLinkDTO) => {
    const newLink = await createLink(dto);
    showToast(`Created shortcut go/${newLink.alias}`);
    await loadLinks();
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this shortcut?')) {
      await deleteLink(id);
      showToast('Shortcut deleted');
      await loadLinks();
    }
  };

  const handleCopy = (url: string) => {
    navigator.clipboard.writeText(url);
    const id = links.find((l) => url.includes(l.alias))?.id || null;
    setCopiedId(id);
    showToast(`Copied ${url} to clipboard!`);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="container">
      <Header onOpenCreateModal={() => setIsModalOpen(true)} />

      <StatsOverview links={links} />

      <div className="controls-bar">
        <div className="search-input-wrapper">
          <Search size={18} className="search-icon" />
          <input
            type="text"
            className="search-input"
            placeholder="Search shortcuts by alias, title, target URL, or tag..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <select
          className="sort-select"
          value={sortBy}
          onChange={(e: any) => setSortBy(e.target.value)}
        >
          <option value="createdAt">Newest First</option>
          <option value="clickCount">Most Popular (Clicks)</option>
          <option value="alias">Alphabetical (Alias)</option>
        </select>
      </div>

      {loading && links.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-muted)' }}>
          Loading shortcuts...
        </div>
      ) : links.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '4rem', background: 'var(--bg-card)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-color)' }}>
          <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>No Go Links Found</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            {search ? `No shortcuts match "${search}"` : 'Get started by creating your first internal shortcut link!'}
          </p>
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            Create Shortcut
          </button>
        </div>
      ) : (
        <div className="links-grid">
          {links.map((link) => (
            <LinkCard
              key={link.id}
              link={link}
              onDelete={handleDelete}
              onCopy={handleCopy}
              copiedId={copiedId}
            />
          ))}
        </div>
      )}

      <CreateModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreate}
      />

      {toastMessage && (
        <div className="toast">
          <Check size={18} />
          {toastMessage}
        </div>
      )}
    </div>
  );
};

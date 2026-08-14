import { GoLink, CreateGoLinkDTO, ApiResponse } from '../types';

const API_BASE = '/api/v1';

export async function fetchLinks(search?: string, tag?: string, sortBy?: string): Promise<GoLink[]> {
  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (tag) params.append('tag', tag);
  if (sortBy) params.append('sortBy', sortBy);

  const res = await fetch(`${API_BASE}/links?${params.toString()}`);
  const json: ApiResponse<GoLink[]> = await res.json();

  if (!json.success || !json.data) {
    throw new Error(json.error?.message || 'Failed to fetch shortcuts');
  }

  return json.data;
}

export async function createLink(dto: CreateGoLinkDTO): Promise<GoLink> {
  const res = await fetch(`${API_BASE}/links`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dto),
  });

  const json: ApiResponse<GoLink> = await res.json();

  if (!json.success || !json.data) {
    const errorMsg = json.error?.details
      ? Array.isArray(json.error.details)
        ? json.error.details.map((d: any) => d.message).join(', ')
        : json.error.message
      : json.error?.message || 'Failed to create shortcut';
    throw new Error(errorMsg);
  }

  return json.data;
}

export async function deleteLink(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/links/${id}`, {
    method: 'DELETE',
  });

  const json: ApiResponse<null> = await res.json();

  if (!json.success) {
    throw new Error(json.error?.message || 'Failed to delete shortcut');
  }
}

export interface GoLink {
  id: string;
  alias: string;
  targetUrl: string;
  title: string;
  description?: string;
  tags: string[];
  clickCount: number;
  lastAccessedAt: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface CreateGoLinkDTO {
  alias: string;
  targetUrl: string;
  title: string;
  description?: string;
  tags?: string[];
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}

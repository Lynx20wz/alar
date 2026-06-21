import type { CommentInfo } from "./Comment";

export interface PostInfo {
  id: number;
  title: string;
  content: string;
  author_id: number;
  is_liked: boolean;
  created_at: Date;
  image: string | null;
  views: number;
}
export interface PostWithCommentsInfo extends PostInfo {
  comments: CommentInfo[];
}

import type { User } from "./User";

export interface Post {
  id: number;
  author: User;
  created_at: string;
  title: string;
  content: string;
  comments: Comment[];
}

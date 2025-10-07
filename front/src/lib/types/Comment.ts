import type { Post } from "./Post";
import type { User } from "./User";

export interface Comment {
  id: number;
  author: User;
  post: Post;
  created_at: string;
  content: string;
}
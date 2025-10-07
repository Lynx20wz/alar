import type { Post } from "./Post";

export interface User {
  id: number;
  username: string;
  email: string;
  followers: User[];
  posts: Post[];
  comments: Comment[];
}

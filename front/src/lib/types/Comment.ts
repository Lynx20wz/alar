import type { UserShortInfo } from "./User";
import type { PostShortInfo } from "./Post";

export interface CommentInfo {
  id: number;
  author: UserShortInfo;
  created_at: Date;
  content: string;
}

export interface CommentInfoWithPost extends CommentInfo {
  post: PostShortInfo;
}
import type { UserShortInfo } from "./User";
import type { CommentInfo } from "./Comment";
import type { LikesInfo } from "./Likes";

export interface PostShortInfo {
  id: number;
  author: UserShortInfo;
  created_at: string;
  title: string;
  views: number;
  is_liked: boolean;
  likes: LikesInfo<UserShortInfo>;
}
export interface PostInfo extends PostShortInfo {
  content: string;
  image: Blob;
  comments: CommentInfo[];
}

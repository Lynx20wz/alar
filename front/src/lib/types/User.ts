import type { PostShortInfo } from "./Post";
import type { CommentInfo } from "./Comment";
import type { LikesInfo } from "./Likes";
import type { SocialLinkInfo, StackInfo } from "./Others";

export interface UserShortInfo {
  id: number;
  username: string;
}
export interface UserInfo extends UserShortInfo {
  email: string;
  bio: string | null;
  follows: LikesInfo<UserShortInfo>;
  followers: LikesInfo<UserShortInfo>;
  posts: PostShortInfo[];
  comments: CommentInfo[];
  social_links: SocialLinkInfo[];
  stacks: StackInfo[];
}

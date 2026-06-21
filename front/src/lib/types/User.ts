import type { SocialLinkInfo, StackInfo } from "./Others";

export interface UserShortInfo {
  id: number;
  username: string;
  email: string;
  bio: string | null;
}
export interface UserInfo extends UserShortInfo {
  social_links: SocialLinkInfo[];
  stacks: StackInfo[];
}

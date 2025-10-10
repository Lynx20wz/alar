export interface SocialLinkInfo {
  id: number;
  user_id: number;
  platform: string;
  url: string;
}

export interface StackInfo {
  id: number;
  user_id: number;
  title: string;
  icon: Blob;
  url: string;
}

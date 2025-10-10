enum LikesType {
    users = "users",
    posts = "posts",
    comments = "comments"
}

export interface TotalInfo {
    total: number;
}

export interface LikesInfo<T> extends TotalInfo {
    type: LikesType;
    objects: T[];
}
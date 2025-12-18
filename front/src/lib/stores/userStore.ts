import { writable } from "svelte/store";
import type { UserInfo } from "../types/User";

export const user = writable<UserInfo | null>(null);

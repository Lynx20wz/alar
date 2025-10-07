import { writable } from "svelte/store";
import type { User } from "../types/User";

export const user = writable<User | null>(null);

# 🧵 Procedural Jersey Generator

⚽ Procedural Jersey Generator — A mini compiler project for CS152  
_A Domain-Specific Language (DSL) for Soccer Kit Design_

### 👨‍💻 Author

**Ben Nguyen**  
CS 152 – Programming Languages, Fall 2025  
San José State University

---

## 📖 Overview

This project implements a **small domain-specific language (DSL)** that lets users
describe and generate soccer jerseys using simple text commands.

A jersey description looks like this:

```txt
jersey {
  team: "Spartan FC";
  primary: #000958;
  secondary: #FF5B2E;
  pattern: stripes(7,14);
  number: 23;
  player: "BEN";
  sponsor: "San Jose State University";
  font: "Inter", 28;
  badge: left;
  output: "spartan_fc.svg";
}
```

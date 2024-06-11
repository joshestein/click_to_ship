export class Peter extends HTMLDivElement {
  constructor() {
    super();
  }
}

customElements.define("peter", Peter);

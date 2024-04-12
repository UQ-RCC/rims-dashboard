export const tablePerPageSetupMixin = {
    computed: {
        tableItemsPerPage() {
            if (this.$vuetify.breakpoint.mdAndDown) {
                return 5;
            } else if (this.$vuetify.breakpoint.lgAndDown) {
                return 10;
            } else {
                return 14;
            }
        },
        tableRowOptions() {
            if (this.tableItemsPerPage <= 5) {
                return [2, this.tableItemsPerPage, Math.round(this.tableItemsPerPage*2/10)*10, 50, -1]
            } else if (this.tableItemsPerPage <= 10) {
                return [5, this.tableItemsPerPage, Math.round(this.tableItemsPerPage*2/10)*10, 50, -1]
            } else {
                return [Math.round(this.tableItemsPerPage/2/10)*10, this.tableItemsPerPage, Math.round(this.tableItemsPerPage*2/10)*10, 100, -1];
            }
        }            
    }
}
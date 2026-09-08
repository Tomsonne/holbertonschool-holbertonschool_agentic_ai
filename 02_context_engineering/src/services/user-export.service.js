const userRepository = require('../repositories/user.repository');

class UserExportService {
    async exportUserByEmail(email) {
        const user = userRepository.findByEmail(email);
        if (!user) {
            throw new Error("Utilisateur introuvable dans le système");
        }
        return JSON.stringify(user);
    }
}

module.exports = new UserExportService();

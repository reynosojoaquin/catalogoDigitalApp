import express from 'express';
import bancaRoutes from '../routes/Banca';
import clienteRoutes from '../routes/Cliente';
import contactoRoutes from '../routes/Contacto';
import consorcioRoutes from '../routes/Consorcio';
import personaRoutes from '../routes/Persona';
import vendedorRoutes from '../routes/Vendedor';
import terminalRoutes from '../routes/Terminal';
import jugadaRoutes from '../routes/Jugada';
import detalleJugadaRoutes from '../routes/DetalleJugada';
import tipoJuegoRoutes from '../routes/TipoJuego';
import InventarioBancaRoutes from '../routes/InventarioBanca';
import LoteriaRoutes from '../routes/Loteria';
import InventarioTerminalRoutes from '../routes/InventarioTerminal';
import rolRoutes from '../routes/Rol';
import permisoRoutes from '../routes/Permiso';
import usuarioRoutes from '../routes/Permiso';
import direccionRoutes from '../routes/Direccion';
import telefonoRoutes from '../routes/Telefono';
import tipoDireccionRoutes from '../routes/TipoDireccion';
import tipoTelefonoRoutes     from '../routes/TipoTelefono';
import sectorRoutes from '../routes/Sector';
import ciudadRoutes from '../routes/Ciudad';
import provinciaRoutes from '../routes/Provincia';
import tipoContactoRoutes from '../routes/TipoContacto';
// Initialization
let router = express.Router();

// Routes
router.use('/cliente', clienteRoutes);
router.use('/persona', personaRoutes);
router.use('/contacto', contactoRoutes);
router.use('/consorcio', consorcioRoutes);
router.use('/banca', bancaRoutes);
router.use('/terminal', terminalRoutes);
router.use('/vendedor', vendedorRoutes);
router.use('/jugada', jugadaRoutes);
router.use('/detallejugada', detalleJugadaRoutes);
router.use('/tipojuego', tipoJuegoRoutes);
router.use('/inventariobanca', InventarioBancaRoutes);
router.use('/loteria', LoteriaRoutes);
router.use('/inventarioterminal', InventarioTerminalRoutes);
router.use('/rol', rolRoutes);
router.use('/permiso', permisoRoutes);
router.use('/usuario', usuarioRoutes);
router.use('/direccion', direccionRoutes);
router.use('/telefono', telefonoRoutes);
router.use('/tipoDireccion', tipoDireccionRoutes);
router.use('/tipoTelefono', tipoTelefonoRoutes);
router.use('/sector', sectorRoutes);
router.use('/provincia', provinciaRoutes);
router.use('/ciudad', ciudadRoutes);
router.use('/tipoContacto', tipoContactoRoutes);

export default router;
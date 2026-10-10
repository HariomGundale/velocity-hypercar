// Single source of truth: backend car -> how it is shown. The BACKEND decides which car it is; this file only says
// where that car's 3D model lives and how to read it. Matching is exact (slug, then exact normalised name):
// a car is never shown with another car's model.
import {resolveAssetUrl,API_BASE_URL} from './services/api.js';

export const normalizeCarKey=s=>String(s||'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
const BASE=import.meta.env.BASE_URL;

const REGISTRY=[
 {key:'porsche-911-gt3-rs',alt:'Porsche 911 GT3 RS',art:'gt3rs',slugs:['porsche-911-gt3-rs'],names:['porsche-911-gt3-rs'],model:{credit:''}},
 {key:'suzuki-swift',alt:'Suzuki Swift',art:'swift',slugs:['suzuki-swift'],names:['suzuki-swift'],model:{credit:''}},
 {key:'ferrari-296-gtb',alt:'Ferrari 296 GTB',art:'ferrari',slugs:['ferrari-296-gtb'],names:['ferrari-296-gtb'],model:{credit:''}},
 {key:'glc-300e',alt:'Mercedes-Benz GLC 300e',art:'glc',slugs:['glc-300e'],names:['glc-300e','mercedes-benz-glc-300e'],model:{credit:''}},
 {key:'lamborghini-huracan-tecnica',alt:'Lamborghini Huracán Tecnica',art:'huracan',slugs:['lamborghini-huracan-tecnica'],names:['lamborghini-huracan-tecnica'],model:{credit:''}},
 {key:'eqs-580',alt:'Mercedes-Benz EQS 580',art:'eqs',slugs:['eqs-580'],names:['eqs-580','mercedes-benz-eqs-580'],model:{credit:''}},
 {key:'mazda-3',alt:'Mazda 3',art:'mazda',slugs:['mazda-3'],names:['mazda-3'],model:{credit:''}}];

const find=car=>{const slug=normalizeCarKey(car.slug),name=normalizeCarKey(car.name);
 return REGISTRY.find(r=>slug&&r.slugs.includes(slug))||REGISTRY.find(r=>name&&r.names.includes(name))||null};

export function resolveVehicleVisual(car){
 const c=car||{},entry=find(c),slug=entry?entry.slugs[0]:normalizeCarKey(c.slug||c.name),cfg=entry?.model||{},backendImage=resolveAssetUrl(c.image_url);
 
 const models=[`${API_BASE_URL}/assets/models/${slug}.glb`,`${BASE}models/cars/${slug}.glb`].map(url=>({url,cfg,credit:cfg.credit}));
 return{models,key:entry?.key||slug||'unknown',alt:entry?.alt||c.name||'Vehicle',sources:backendImage?[backendImage]:[],art:entry?.art||null}}

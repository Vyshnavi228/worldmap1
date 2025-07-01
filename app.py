// WikiWorldMap: Interactive Country Knowledge App (Basic Version)

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

const WikiWorldMap = () => {
  const [countryData, setCountryData] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState(null);

  const fetchWikiSummary = async (countryName) => {
    try {
      const response = await axios.get(
        `https://en.wikipedia.org/w/api.php`,
        {
          params: {
            action: 'query',
            prop: 'extracts',
            exintro: true,
            titles: countryName,
            format: 'json',
            origin: '*'
          }
        }
      );
      const pages = response.data.query.pages;
      const page = pages[Object.keys(pages)[0]];
      return page.extract;
    } catch (error) {
      console.error("Error fetching Wikipedia summary:", error);
      return "Summary not available.";
    }
  };

  const onEachCountry = (feature, layer) => {
    layer.on({
      click: async () => {
        const countryName = feature.properties.ADMIN;
        const summary = await fetchWikiSummary(countryName);
        setSelectedCountry({ name: countryName, summary });
      }
    });
  };

  useEffect(() => {
    const fetchGeoData = async () => {
      try {
        const response = await axios.get('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json');
        setCountryData(response.data);
      } catch (error) {
        console.error("Error loading geo data:", error);
      }
    };
    fetchGeoData();
  }, []);

  return (
    <div className="h-screen w-screen flex">
      <div className="w-2/3 h-full">
        <MapContainer style={{ height: "100%", width: "100%" }} center={[20, 0]} zoom={2}>
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {countryData && (
            <GeoJSON data={countryData} onEachFeature={onEachCountry} />
          )}
        </MapContainer>
      </div>
      <div className="w-1/3 p-4 bg-gray-100 overflow-y-auto">
        {selectedCountry ? (
          <div>
            <h2 className="text-2xl font-bold mb-2">{selectedCountry.name}</h2>
            <div dangerouslySetInnerHTML={{ __html: selectedCountry.summary }} />
          </div>
        ) : (
          <p className="text-gray-600">Click on a country to see its Wikipedia summary.</p>
        )}
      </div>
    </div>
  );
};

export default WikiWorldMap;

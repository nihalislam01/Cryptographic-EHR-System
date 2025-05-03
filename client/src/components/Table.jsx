import { useEffect, useState } from "react";

function Table({keys, rows, renderActions, onRowClick }) {

    const [searchTerm, setSearchTerm] = useState("");
    const [filteredRows, setFilteredRows] = useState(rows);

    useEffect(() => {
        setFilteredRows(rows);
      }, [rows]);

    const handleSearch = (e) => {
        const value = e.target.value.toLowerCase();
        setSearchTerm(value);
    
        const filtered = rows.filter((row) =>
          keys.some((key) =>
            String(row[key]).toLowerCase().includes(value)
          )
        );
    
        setFilteredRows(filtered);
      };

    return (
        <>
        <div className="d-flex align-items-center">
            <input type="text" className="w-100 text-center" style={{fontFamily: 'Arial, FontAwesome'}} placeholder="Search" name="search" value={searchTerm} onChange={handleSearch} />
        </div>
        <hr />
        <table className="table text-center">
            <thead>
                <tr>
                    {keys.map((key, index)=>(
                        <th key={index}>{key.toUpperCase()}</th>
                    ))}
                    {renderActions && <th>ACTIONS</th>}
                </tr>
            </thead>
            <tbody>
                {filteredRows.map((row, index)=>(
                    <tr key={index} style={{cursor: onRowClick?  "pointer":""}} onClick={onRowClick ? () => onRowClick(row._id) : undefined} >
                        {keys.map((key, index)=>(
                        <td key={index}>{
                            key === 'verified' ? (
                            row[key] ? (
                                <span style={{fontSize: "13px", backgroundColor: "rgb(95, 176, 72, 0.7)", border: "1px solid rgb(95, 176, 72)", padding: "2px 5px", color: "white", borderRadius: "25px"}}>Doctor Verified</span>
                            ) : (
                                <span style={{fontSize: "13px", backgroundColor: "rgb(157, 2, 8, 0.7)", border: "1px solid rgb(157, 2, 8)", padding: "2px 5px", color: "white", borderRadius: "25px"}}>Not Doctor Verified</span>
                            )
                        ) : (
                            row[key]
                        )}</td>
                        ))}
                        {renderActions && (
                            <td onClick={(e) => {e.stopPropagation();}}>{renderActions(row)}</td>
                        )}
                    </tr>
                ))}
            </tbody>
        </table>
        </>
    )
}

export default Table;